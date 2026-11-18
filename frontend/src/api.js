import axios from "axios";

const API_BASE = "http://localhost:5000/api";

export const registerPerson = (name, images) =>
  axios.post(`${API_BASE}/register`, { name, images }).then((res) => res.data);

export const recognizeFace = (image) =>
  axios.post(`${API_BASE}/recognize`, { image }).then((res) => res.data);

export const getHistory = (limit = 50) =>
  axios.get(`${API_BASE}/history`, { params: { limit } }).then((res) => res.data);

export const getDashboardStats = () =>
  axios.get(`${API_BASE}/dashboard`).then((res) => res.data);

export const getPersons = () =>
  axios.get(`${API_BASE}/persons`).then((res) => res.data);
