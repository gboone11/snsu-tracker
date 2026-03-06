import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
});

export const apiService = {
  getStatus: async () => {
    console.log("API: getStatus called");
    const response = await api.get("/api/status");
    console.log("API: getStatus response", response.data);
    return response;
  },

};
