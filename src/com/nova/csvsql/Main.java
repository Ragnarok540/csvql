package com.nova.csvsql;

import java.sql.*;
import java.util.*;

public class Main {

	public static void main(String[] args) {
		List<String[]> table = CSV.loadFile("csv_data.csv");		
		Connection connection = null;
		Statement statement = null;
		
		try {
			connection = DB.createSQLiteConnection("cars.db");
			System.out.println("\nBase de datos creada y conectada!\n");
		} catch (SQLException e) {
			System.out.println("\nLa base de datos no pudo ser creada!\n");
			e.printStackTrace();
		}
		
		try {
			statement = DB.createStatement(connection, 30);
			System.out.println("\nLa base de datos está lista!\n");
		} catch (SQLException e) {
			System.out.println("\nLa base de datos no está lista!\n");
			e.printStackTrace();
		}
		
		try {
			statement.executeUpdate(DB.dropTable("CARS"));
			statement.executeUpdate(DB.createTable("CARS", table));
			System.out.println("\nTabla creada correctamente!\n");
		} catch (SQLException e) {
			System.out.println("\nError al crear la tabla!\n");
			e.printStackTrace();
		}
		
		try {
			statement.executeUpdate(DB.bulkInsert("CARS", table));
			System.out.println("\nRegistros insertados correctamente!\n");
		} catch (SQLException e) {
			System.out.println("\nError al insertar registros!\n");
			e.printStackTrace();
		}
		
		ResultSet rs = null;
		String query = null;
		
		try {
			//query = "SELECT * FROM CARS WHERE MAKE = 'VOLVO'";
			query = "SELECT MAKE, COUNT(*) FROM CARS GROUP BY MAKE ORDER BY COUNT(*) DESC";
			rs = statement.executeQuery(query);
			System.out.println("Consulta: " + query + "\n");
			System.out.println(DB.getPrintableResult(rs, ','));
			System.out.println("\nConsulta ejecutada correctamente!\n");
		} catch (SQLException e) {
			System.out.println("\nError al ejecutar la consulta!\n");
			e.printStackTrace();
		}
		
		try {
			rs = statement.executeQuery(query);
			CSV.saveFile(DB.getTable(rs), "result.csv");
			System.out.println("\nResultado guardado correctamente!\n");
		} catch (SQLException e) {
			System.out.println("\nError al guardar el resultado!\n");
			e.printStackTrace();
		}	

	}

}
