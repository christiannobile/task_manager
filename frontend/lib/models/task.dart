class Task {
  final String? id;
  final String title;
  final String description;
  final String? dueDate;
  final bool completed;

  Task({
    this.id,
    required this.title,
    this.description = '',
    this.dueDate,
    this.completed = false,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'],
      title: json['title'],
      description: json['description'] ?? '',
      dueDate: json['due_date'],
      completed: json['completed'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      'title': title,
      'description': description,
      'due_date': dueDate,
      'completed': completed,
    };
  }
}
