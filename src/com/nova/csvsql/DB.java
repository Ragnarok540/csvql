package com.nova.csvsql;

import java.sql.*;
import java.util.*;

public class DB {

	public static Connection createSQLiteConnection(String name) throws SQLException {
		Connection connection = null;
		
		try {
			Class.forName("org.sqlite.JDBC");
			connection = DriverManager.getConnection("jdbc:sqlite:" + name);
		} catch (ClassNotFoundException e) {
			System.out.println("\nError con la libreria SQLite!\n");
			e.printStackTrace();
		}
		return connection;
	}

	public static Statement createStatement(Connection connection, int timeout) throws SQLException {
		Statement statement = connection.createStatement();
		statement.setQueryTimeout(timeout);
		return statement;
	}

	public static String createTable(String tableName, List<String[]> table) {
		int columns = table.get(0).length;
		StringBuilder sb = new StringBuilder();
		String[] columnNames = detColumnNames(table).split(",");
		String[] types = detTypes(table).split(",");
		sb.append("CREATE TABLE ");
		sb.append(tableName);
		sb.append(" (");
		
		for (int c = 0; c < columns; c++) {
			sb.append(columnNames[c]);
			sb.append(" ");
			sb.append(types[c]);
			
			if (c < (columns - 1)) {
				sb.append(", ");
			}
		}
		
		sb.append(")");
		return sb.toString();
	}
		
	public static String insertRow(String tableName, String[] row) {
		int columns = row.length;
		StringBuilder sb = new StringBuilder();
		String tipo = null;
		sb.append("INSERT INTO ");
		sb.append(tableName);
		sb.append(" VALUES (");
		
		for (int c = 0; c < columns; c++) {
			tipo = detTypeValue(row[c]);
			
			if (tipo.equals("NULL")) {
				sb.append("NULL");
			} else {
				sb.append("'");
				sb.append(row[c]);
				sb.append("'");
			}
						
			if (c < (columns - 1)) {
				sb.append(", ");
			}
		}
		
		sb.append("); ");
		return sb.toString();
	}
	
	public static String bulkInsert(String tableName, List<String[]> table) {
		Iterator<String[]> rows = table.iterator();
		String[] row;
		String[] header = rows.next();
		StringBuilder sb = new StringBuilder();
		int columns = header.length;
		String tipo = null;
		sb.append("INSERT INTO ");
		sb.append(tableName);
		sb.append(" VALUES ");
		
		while (rows.hasNext()) {
			row = rows.next();
			sb.append("(");
			
			for (int c = 0; c < columns; c++) {
				tipo = detTypeValue(row[c]);
				
				if (tipo.equals("NULL")) {
					sb.append("NULL");
				} else {
					sb.append("'");
					sb.append(row[c]);
					sb.append("'");
				}
							
				if (c < (columns - 1)) {
					sb.append(", ");
				}
			}
			
			sb.append("), ");
		}
		
		sb.setCharAt(sb.length() - 2, ';');
		
		return sb.toString();
	}
	
	public static String dropTable(String name) {
		return "DROP TABLE IF EXISTS " + name;
	}

	public static String detTypeValue(String value) {
		if (value.equals("")) return "NULL";

		try {
			Integer.parseInt(value);
			return "INTEGER";
		} catch (NumberFormatException e) { }

		try {
			Double.parseDouble(value);
			return "REAL";
		} catch (NumberFormatException e) { }

		return "TEXT";
	}

	public static String detTypeColumn(List<String[]> table, int i) {
		Iterator<String[]> rows = table.iterator();
		String[] row;
		String type;
		boolean integer = false, real = false, text = false;
		rows.next(); // header
		
		while (rows.hasNext()) {
			row = rows.next();
			type = detTypeValue(row[i]);
			
			switch (type) {
				case "INTEGER": integer = true;
					break;
				case "REAL": real = true;
					break;
				case "TEXT": text = true;
					break;
				default: 
					break;
			}
		}
		
		if (text == true) return "TEXT";
		if (real == true) return "REAL";
		if (integer == true) return "INTEGER";
		return "TEXT";
	}
	
	public static String detTypes(List<String[]> table) {
		int i = table.get(0).length; 
		StringBuilder sb = new StringBuilder();
		
		for (int c = 0; c < i; c++) {
			sb.append(detTypeColumn(table, c));
			sb.append(",");
		}
		
		return sb.toString();
	}
	
	public static String detColumnNames(List<String[]> table) {
		int i = table.get(0).length; // header
		StringBuilder sb = new StringBuilder();
		
		for (int c = 0; c < i; c++) {
			sb.append(table.get(0)[c]);
			sb.append(",");
		}
		
		return sb.toString();
	}
	
	public static String getPrintableResult(ResultSet rs, char separator) throws SQLException {
		ResultSetMetaData rsmd = rs.getMetaData();
		int columns = rsmd.getColumnCount();
		StringBuilder sb = new StringBuilder();
				
		for (int c = 0; c < columns; c++) {
			sb.append(rsmd.getColumnLabel(c + 1).toUpperCase());
			
			if (c < (columns - 1)) {
				sb.append(separator);
			}
		}
		
		sb.append("\n");		
		
		while (rs.next()) {
			for (int c = 0; c < columns; c++) {
				sb.append(rs.getString(c + 1));
								
				if (c < (columns - 1)) {
					sb.append(separator);
				}
			}
			
			sb.append("\n");	
		}
		
		return sb.toString();
	}
	
	public static List<String[]> getTable(ResultSet rs) throws SQLException {
		List<String[]> table = new ArrayList<String[]>();
		ResultSetMetaData rsmd = rs.getMetaData();
		int columns = rsmd.getColumnCount();
		String[] row = new String[columns];	
				
		for (int c = 0; c < columns; c++) {
			row[c] = rsmd.getColumnLabel(c + 1).toUpperCase();
		}
		
		table.add(row);	
		row = new String[columns];	
		
		while (rs.next()) {
			for (int c = 0; c < columns; c++) {
				row[c] = rs.getString(c + 1);
			}
			
			table.add(row);		
			row = new String[columns];	
		}
		
		return table;
	}

}
