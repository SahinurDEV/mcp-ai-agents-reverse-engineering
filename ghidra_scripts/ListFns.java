// List non-external functions with entry addresses.
// @category MCPCourse
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;

public class ListFns extends GhidraScript {
    @Override
    public void run() throws Exception {
        println("BEGIN_C");
        for (Function f : currentProgram.getFunctionManager().getFunctions(true)) {
            if (f.isExternal() || f.isThunk()) continue;
            System.out.println(f.getEntryPoint() + " " + f.getName());
        }
        println("END_C");
    }
}
