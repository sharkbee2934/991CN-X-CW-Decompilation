// 打印开头若干条指令，用于验证 nxu8 语言是否被 Ghidra 正确加载
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.Listing;

public class Dump extends GhidraScript {
    private void dump(Listing listing, Address start, int count) {
        Address a = start;
        for (int i = 0; i < count && a != null; i++) {
            disassemble(a);
            Instruction ins = listing.getInstructionAt(a);
            if (ins == null) {
                println(String.format("%06X  <无法反汇编>", a.getOffset()));
                return;
            }
            println(String.format("%06X  %-3d %s", a.getOffset(), ins.getLength(), ins.toString()));
            a = ins.getNext() == null ? null : ins.getNext().getAddress();
        }
    }

    @Override
    public void run() throws Exception {
        Listing listing = currentProgram.getListing();
        println("language = " + currentProgram.getLanguageID());
        dump(listing, currentProgram.getMinAddress(), 12);
        println("--- 0x946A (_start) ---");
        dump(listing, currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(0x946A), 8);
    }
}
