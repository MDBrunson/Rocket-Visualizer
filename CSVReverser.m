function CSVReverser(filename)
fhr = fopen(filename, "r");
filename = ['reversed_' filename];
fhw = fopen(filename, 'w');
line = fgets(fhr);
fprintf(fhw, line);
line = fgetl(fhr);
file = "";
while ischar(line)
    file = [file; line];
    line = fgets(fhr);
end

file = file(end:-1:1, :);
for x = 1:length(file)
    fprintf(fhw, file(x));
end

fclose(fhr);
fclose(fhw);
end