import React from "react";
import { ApolloClient, InMemoryCache, ApolloProvider, useQuery, gql, useMutation } from "@apollo/client";

const client = new ApolloClient({
  uri: "http://localhost:5000/graphql",
  cache: new InMemoryCache()
});

const GET_TASKS = gql`
  query GetTasks {
    tasks {
      id
      title
      description
      completed
    }
  }
`;

const CREATE_TASK = gql`
  mutation CreateTask($title: String!, $description: String) {
    createTask(title: $title, description: $description) {
      task {
        id
        title
        description
        completed
      }
    }
  }
`;

function TaskList() {
  const { loading, error, data, refetch } = useQuery(GET_TASKS);
  const [createTask] = useMutation(CREATE_TASK, {
    onCompleted: () => refetch()
  });

  const [title, setTitle] = React.useState("");
  const [description, setDescription] = React.useState("");

  const handleAdd = () => {
    if (!title.trim()) return;
    createTask({ variables: { title, description } });
    setTitle("");
    setDescription("");
  };

  return (
    <div style={{padding: 20}}>
      <h2>Task Manager</h2>
      <input
        placeholder="Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
        style={{ marginRight: 8 }}
      />
      <input
        placeholder="Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
        style={{ marginRight: 8 }}
      />
      <button onClick={handleAdd}>Add Task</button>
      {loading && <p>Loading tasks...</p>}
      {error && <p style={{color: "red"}}>Could not load tasks. Backend may be down.</p>}
      <ul>
        {data && data.tasks && data.tasks.map(task => (
          <li key={task.id}>
            <b>{task.title}</b>: {task.description} {task.completed ? "(Done)" : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function App() {
  return (
    <ApolloProvider client={client}>
      <TaskList />
    </ApolloProvider>
  );
}
