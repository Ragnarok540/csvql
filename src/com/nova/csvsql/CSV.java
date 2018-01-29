package com.nova.csvsql;

import com.opencsv.*;
import java.io.*;
import java.util.*;

public class CSV {

	public static List<String[]> loadFile(String path) {
		List<String[]> list = new ArrayList<String[]>();
		final CSVParser PARSER = new CSVParserBuilder()
		.withSeparator(',')
		.withIgnoreQuotations(true)
		.build();
		try {
			final CSVReader READER = new CSVReaderBuilder(new FileReader(path))
			.withCSVParser(PARSER)
			.build();
			String[] fields = null;
            while ((fields = READER.readNext()) != null) {
            	list.add(fields);
            }			
		} catch (FileNotFoundException e) {
			System.out.println("\nEl archivo no fue encontrado!\n");
			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("\nError al leer el archivo!\n");
			e.printStackTrace();
		}
		return list;
	}

	public static void saveFile(List<String[]> list, String path) {
		CSVWriter writer = null;
        try {
        	writer = new CSVWriter(new FileWriter(path), ',');
            writer.writeAll(list, false);
        } catch (IOException e) {
        	System.out.println("\nError al guardar el archivo!\n");
			e.printStackTrace();
		} finally {
			try {
				writer.close();
			} catch (IOException e) {
				System.out.println("\nError al cerrar el escritor!\n");
				e.printStackTrace();
			}
		}
	}

}
