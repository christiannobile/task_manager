from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class TaskModel(db.Model):
    id = db.Column(db.Int, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"

class Task(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    completed = graphene.Boolean()

class Query(graphene.ObjectType):
    tasks = graphene.List(Task)

    def resolve_tasks(root, info):
        tasks = TaskModel.query.all()
        return [Task(id=t.id, title=t.title, description=t.description, completed=t.completed) for t in tasks]

class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
    
    task = graphene.Field(lambda: Task)

    def mutate(root, info, title, description=None):
        new_task = TaskModel(title=title, description=description, completed=False)
        db.session.add(new_task)
        db.session.commit()
        return CreateTask(task=Task(id=new_task.id, title=new_task.title, description=new_task.description, completed=new_task.completed))

class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    task = graphene.Field(lambda: Task)

    def mutate(root, info, id, title=None, description=None, completed=None):
        task = TaskModel.query.get(id)
        if task is None:
            raise Exception("Task not found")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        db.session.commit()
        return UpdateTask(task=Task(id=task.id, title=task.title, description=task.description, completed=task.completed))

class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        task = TaskModel.query.get(id)
        if task is None:
            raise Exception("Task not found")
        db.session.delete(task)
        db.session.commit()
        return DeleteTask(ok=True)

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
