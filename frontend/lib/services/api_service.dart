import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/task.dart';

class ApiService {
  // Change this URL to your backend address:
  static const String baseUrl = 'http://10.0.2.2:8000';

  Future<List<Task>> fetchTasks() async {
    final response = await http.get(Uri.parse('\$baseUrl/tasks'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Task.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load tasks');
    }
  }

  Future<Task> createTask(Task task) async {
    final response = await http.post(Uri.parse('\$baseUrl/tasks'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(task.toJson()));
    if (response.statusCode == 200) {
      return Task.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create task');
    }
  }

  Future<Task> updateTask(Task task) async {
    final response = await http.put(Uri.parse('\$baseUrl/tasks/\${task.id}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(task.toJson()));
    if (response.statusCode == 200) {
      return Task.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to update task');
    }
  }

  Future<void> deleteTask(String id) async {
    final response = await http.delete(Uri.parse('\$baseUrl/tasks/\$id'));
    if (response.statusCode != 200) {
      throw Exception('Failed to delete task');
    }
  }
}
