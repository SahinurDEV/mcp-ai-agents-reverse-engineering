// Decompile one function (arg 0, default "check") and print C to stdout.
// @category MCPCourse
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;

public class DecompileFn extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        String name = a.length > 0 ? a[0] : "check";
        DecompInterface d = new DecompInterface();
        d.openProgram(currentProgram);
        for (Function f : currentProgram.getFunctionManager().getFunctions(true)) {
            if (f.getName().equals(name)) {
                DecompileResults r = d.decompileFunction(f, 60, monitor);
                println("BEGIN_C");
                System.out.println(r.getDecompiledFunction().getC());
                println("END_C");
                return;
            }
        }
        println("function not found: " + name);
    }
}
