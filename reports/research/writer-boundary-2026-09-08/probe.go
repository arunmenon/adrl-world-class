// Synthetic namespace lifetime observations. Primary: ADRL-SAF-007; secondary: ADRL-OPS-001.
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
	"time"
)

func save(name string, value any) {
	data, err := json.Marshal(value)
	if err != nil {
		panic(err)
	}
	if err = os.WriteFile("/work/"+name, data, 0600); err != nil {
		panic(err)
	}
}

func context() map[string]any {
	data, err := os.ReadFile("/proc/self/status")
	if err != nil {
		panic(err)
	}
	v := map[string]any{"pid": os.Getpid(), "uid": os.Getuid(), "gid": os.Getgid()}
	for _, line := range strings.Split(string(data), "\n") {
		key, val, ok := strings.Cut(line, ":")
		if ok && (key == "CapEff" || key == "NoNewPrivs" || key == "Seccomp" || key == "Seccomp_filters" || key == "NSpid") {
			v[key] = strings.TrimSpace(val)
		}
	}
	for _, path := range []string{"/proc/self/cgroup", "/sys/fs/cgroup/cgroup.events"} {
		data, err := os.ReadFile(path)
		v[path] = map[string]any{"readable": err == nil, "data": string(data)}
	}
	_, err = os.Stat("/var/run/docker.sock")
	v["docker_socket_present"] = err == nil
	_, err = os.Stat("/sys/fs/cgroup/cgroup.kill")
	v["cgroup_kill_present"] = err == nil
	f, err := os.OpenFile("/sys/fs/cgroup/cgroup.procs", os.O_WRONLY, 0)
	v["cgroup_migration_open_allowed"] = err == nil
	if err == nil {
		f.Close()
	}
	return v
}

func main() {
	// Every admitted mode is self-terminating even if the host observer disappears.
	time.AfterFunc(7*time.Second, func() { os.Exit(99) })
	if len(os.Args) < 2 {
		panic("mode required")
	}
	mode := os.Args[1]
	if mode == "child" {
		delay, err := strconv.Atoi(os.Args[2])
		if err != nil {
			panic(err)
		}
		f, err := os.OpenFile("/work/late.txt", os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0600)
		if err != nil {
			panic(err)
		}
		defer f.Close()
		group, err := syscall.Getpgid(0)
		if err != nil {
			panic(err)
		}
		save("child-ready.json", map[string]any{"pid": os.Getpid(), "ppid": os.Getppid(), "group": group})
		time.Sleep(time.Duration(delay) * time.Millisecond)
		if _, err = f.WriteString("detached-late-write"); err != nil {
			panic(err)
		}
		if err = f.Sync(); err != nil {
			panic(err)
		}
		return
	}
	if mode != "positive" && mode != "init_exit" && mode != "forced_stop" && mode != "client_death" {
		panic("invalid mode")
	}
	save("context.json", context())
	delay := "2500"
	if mode == "positive" {
		delay = "400"
	}
	cmd := exec.Command("/probe", "child", delay)
	cmd.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
	cmd.Env = []string{"PATH=/", "LANG=C", "GOMAXPROCS=2"}
	if err := cmd.Start(); err != nil {
		panic(err)
	}
	deadline := time.Now().Add(2 * time.Second)
	for {
		if _, err := os.Stat("/work/child-ready.json"); err == nil {
			break
		}
		if time.Now().After(deadline) {
			panic("child readiness deadline")
		}
		time.Sleep(10 * time.Millisecond)
	}
	save("ready.json", map[string]any{"mode": mode, "child_pid": cmd.Process.Pid, "parent_pid": os.Getpid()})
	if mode == "positive" {
		if err := cmd.Wait(); err != nil {
			panic(err)
		}
		return
	}
	if mode == "init_exit" {
		return
	}
	fmt.Println("fixture-ready")
	time.Sleep(6 * time.Second)
}
