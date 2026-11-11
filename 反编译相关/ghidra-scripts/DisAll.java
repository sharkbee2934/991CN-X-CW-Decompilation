// 前置脚本：把整个 ROM 反汇编出来，供后续自动分析建函数
import ghidra.app.script.GhidraScript;
import ghidra.program.disassemble.Disassembler;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.mem.MemoryBlock;

public class DisAll extends GhidraScript {
    @Override
    public void run() throws Exception {
        Disassembler dis = Disassembler.getDisassembler(currentProgram, monitor, null);
        for (MemoryBlock b : currentProgram.getMemory().getBlocks()) {
            if (!b.isInitialized() || !b.isExecute()) {
                // 未标为可执行的块也照做，ROM 导入后默认都是可执行
            }
            AddressSet set = new AddressSet(b.getStart(), b.getEnd());
            Address a = b.getStart();
            while (a != null && set.contains(a)) {
                dis.disassemble(a, set);
                // 跳到下一条未处理的位置
                ghidra.program.model.listing.Instruction ins =
                    currentProgram.getListing().getInstructionAt(a);
                if (ins != null) {
                    a = ins.getMaxAddress().next();
                } else {
                    a = a.next();
                }
            }
            println("block " + b.getName() + " done");
        }
        println("instructions after pre-pass: " + currentProgram.getListing().getNumInstructions());
    }
}
