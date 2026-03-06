import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
});

export const apiService = {
  lineGroups: {
    create: (data) => api.post('/line-groups', data),
    getAll: () => api.get('/line-groups'),
    getById: (id) => api.get(`/line-groups/${id}`),
    update: (id, data) => api.put(`/line-groups/${id}`, data),
    delete: (id) => api.delete(`/line-groups/${id}`)
  },
  lines: {
    create: (data) => api.post('/lines', data),
    getAll: () => api.get('/lines'),
    getById: (id) => api.get(`/lines/${id}`),
    update: (id, data) => api.put(`/lines/${id}`, data),
    delete: (id) => api.delete(`/lines/${id}`)
  },
  runs: {
    create: (data) => api.post('/runs', data),
    getAll: () => api.get('/runs'),
    getActive: () => api.get('/runs/active'),
    getById: (id) => api.get(`/runs/${id}`),
    update: (id, data) => api.put(`/runs/${id}`, data),
    delete: (id) => api.delete(`/runs/${id}`)
  },
  processSteps: {
    create: (data) => api.post('/process-steps', data),
    getAll: () => api.get('/process-steps'),
    getByGroup: (groupId) => api.get(`/process-steps/group/${groupId}`),
    getById: (id) => api.get(`/process-steps/${id}`),
    update: (id, data) => api.put(`/process-steps/${id}`, data),
    delete: (id) => api.delete(`/process-steps/${id}`)
  },
  stepExecutions: {
    create: (data) => api.post('/step-executions', data),
    getByRun: (runId) => api.get(`/step-executions/run/${runId}`),
    getById: (id) => api.get(`/step-executions/${id}`),
    update: (id, data) => api.put(`/step-executions/${id}`, data),
    delete: (id) => api.delete(`/step-executions/${id}`)
  },
};
