// 对当前程序做两种导出：反编译 C 代码 + Listing ASCII 文本
// 用法：-postScript ExportAll.java <输出路径前缀>
import ghidra.app.script.GhidraScript;
import ghidra.app.util.exporter.AsciiExporter;
import ghidra.app.util.exporter.CppExporter;

import java.io.File;

public class ExportAll extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String base = (args.length > 0) ? args[0] : "export";
        File dir = new File(base).getParentFile();
        if (dir != null && !dir.exists()) {
            dir.mkdirs();
        }

        File cFile = new File(base + ".c");
        boolean okC = new CppExporter().export(cFile, currentProgram, null, monitor);
        println("C++/C export: " + okC + " -> " + cFile.getAbsolutePath() + " (" + cFile.length() + " bytes)");

        File txtFile = new File(base + ".txt");
        boolean okT = new AsciiExporter().export(txtFile, currentProgram, null, monitor);
        println("ASCII export: " + okT + " -> " + txtFile.getAbsolutePath() + " (" + txtFile.length() + " bytes)");

        println("functions = " + currentProgram.getFunctionManager().getFunctionCount());
    }
}
