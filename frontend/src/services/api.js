import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
});

export const apiService = {
  lines: {
    create: (data) => api.post("/lines", data),
    getAll: () => api.get("/lines"),
    getById: (id) => api.get(`/lines/${id}`),
    update: (id, data) => api.put(`/lines/${id}`, data),
    delete: (id) => api.delete(`/lines/${id}`),
    reorder: (orderedIds) =>
      api.put("/lines/reorder", { ordered_ids: orderedIds }),
  },
  runs: {
    create: (data) => api.post("/runs", data),
    getAll: () => api.get("/runs"),
    getActive: () => api.get("/runs/active"),
    getById: (id) => api.get(`/runs/${id}`),
    update: (id, data) => api.put(`/runs/${id}`, data),
    delete: (id) => api.delete(`/runs/${id}`),
  },
  processSteps: {
    create: (data) => api.post("/process-steps", data),
    getAll: () => api.get("/process-steps"),
    getById: (id) => api.get(`/process-steps/${id}`),
    update: (id, data) => api.put(`/process-steps/${id}`, data),
    delete: (id) => api.delete(`/process-steps/${id}`),
    reorder: (orderedIds) =>
      api.put("/process-steps/reorder", { ordered_ids: orderedIds }),
  },
  stepExecutions: {
    create: (data) => api.post("/step-executions", data),
    getByRun: (runId) => api.get(`/step-executions/run/${runId}`),
    getById: (id) => api.get(`/step-executions/${id}`),
    update: (id, data) => api.put(`/step-executions/${id}`, data),
    delete: (id) => api.delete(`/step-executions/${id}`),
  },
  subTasks: {
    create: (data) => api.post("/sub-tasks", data),
    getByExecution: (executionId) =>
      api.get(`/sub-tasks/execution/${executionId}`),
    update: (id, data) => api.put(`/sub-tasks/${id}`, data),
    delete: (id) => api.delete(`/sub-tasks/${id}`),
  },
};
