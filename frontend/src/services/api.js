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
};
