function CSVTrimmer(filename, lines)
fhr = fopen(filename, 'r');
filename = ['trimmed_' filename];
fhw = fopen(filename, 'w');

for x = 1:lines+1
    line = fgets(fhr);
    fprintf(fhw, line);
end
fclose(fhw);
fclose(fhr);
end