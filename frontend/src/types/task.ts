export interface Task {
  id: string;
  title: string;
}

export interface CreateTaskResponse {
  status: string;
  id: string;
}