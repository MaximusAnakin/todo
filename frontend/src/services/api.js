const API_URL = import.meta.env.VITE_API_BASE_URL;

export const createTask = async (title) => {
  const response = await fetch(`${API_URL}/CreateTask`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title }),
  });
  return response.json();
};

export const listTasks = async () => {
  const response = await fetch(`${API_URL}/ListTasks`);
  return response.json();
};