import 'package:flutter/material.dart';
import '../models/task.dart';
import '../services/api_service.dart';
import '../widgets/task_tile.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService apiService = ApiService();
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();

  List<Task> tasks = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadTasks();
  }

  Future<void> loadTasks() async {
    try {
      final fetchedTasks = await apiService.fetchTasks();
      setState(() {
        tasks = fetchedTasks;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading tasks: \$e')));
    }
  }

  Future<void> addTask() async {
    if (_titleController.text.trim().isEmpty) return;

    final newTask = Task(
      title: _titleController.text.trim(),
      description: _descriptionController.text.trim(),
    );

    try {
      final createdTask = await apiService.createTask(newTask);
      setState(() {
        tasks.add(createdTask);
        _titleController.clear();
        _descriptionController.clear();
      });
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Error adding task: \$e')));
    }
  }

  Future<void> toggleComplete(Task task) async {
    final updatedTask = Task(
      id: task.id,
      title: task.title,
      description: task.description,
      dueDate: task.dueDate,
      completed: !task.completed,
    );

    try {
      final result = await apiService.updateTask(updatedTask);
      setState(() {
        final index = tasks.indexWhere((t) => t.id == task.id);
        if (index != -1) tasks[index] = result;
      });
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Error updating task: \$e')));
    }
  }

  Future<void> deleteTask(String id) async {
    try {
      await apiService.deleteTask(id);
      setState(() {
        tasks.removeWhere((task) => task.id == id);
      });
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Error deleting task: \$e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Task Manager')),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Padding(
                  padding: EdgeInsets.all(8),
                  child: Column(
                    children: [
                      TextField(
                        controller: _titleController,
                        decoration: InputDecoration(labelText: 'Task Title'),
                      ),
                      TextField(
                        controller: _descriptionController,
                        decoration: InputDecoration(labelText: 'Description'),
                      ),
                      SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: addTask,
                        child: Text('Add Task'),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: tasks.length,
                    itemBuilder: (context, index) {
                      final task = tasks[index];
                      return TaskTile(
                        task: task,
                        onToggleComplete: () => toggleComplete(task),
                        onDelete: () => deleteTask(task.id!),
                      );
                    },
                  ),
                ),
              ],
            ),
    );
  }
}
