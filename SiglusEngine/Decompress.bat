MD Scene_ss
for %%a in (Scene_UnDecompressed\*.undecompressed) do start ssDecompresser.py "%%~a" "Scene_ss\%%~na"