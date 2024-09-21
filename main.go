package main

import (
	"fmt"
	"os"

	"src.elv.sh/pkg/eval"
	"src.elv.sh/pkg/parse"
)

func stage(fm *eval.Frame, name string, code eval.Callable) error {
	fmt.Printf("Stage: %s {\n", name)
	err := code.Call(fm, []any{}, map[string]any{})
	fmt.Printf("} // Stage: %s\n", name)
	return err
}

func main() {
	// parse arguments, make sure we're good (arg[1] is file, arg[2:] are parameters)
	if len(os.Args) < 1 {
		fmt.Printf("usage: %s <file> [<arg>...]\n", os.Args[0])
		os.Exit(1)
	}
	script_file := os.Args[1]
	script_contents, err := os.ReadFile(script_file)
	if err != nil {
		fmt.Printf("error: failed to read file '%s'\n", script_file)
		os.Exit(1)
	}
	// TODO parse arguments

	// TODO create module/NS with custom builtins
	ns_builder := eval.BuildNs()
	ns_builder.AddGoFns(map[string]any{"stage": stage})
	//ns := ns_builder.Ns()
	// TODO create evaler with such module (and other stuff?)
	ev := eval.NewEvaler()
	ev.ExtendBuiltin(ns_builder)	// should work?
	// run code
	// mostly copied from elvish's source
	src := parse.Source{
		Name: script_file,
		Code: string(script_contents),
		IsFile: true}
	ports, cleanup := eval.PortsFromFiles(
		[3]*os.File{os.Stdin, os.Stdout, os.Stderr},
		ev.ValuePrefix())
	defer cleanup()
	ctx, done := eval.ListenInterrupts()
	err = ev.Eval(src, eval.EvalCfg{
		Ports: ports, Interrupts: ctx, PutInFg: true})
	done()
	if err != nil {
		panic(err)
	}
	os.Exit(0)
}

