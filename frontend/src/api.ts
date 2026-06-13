// src/services/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export const fetchMarketData = async () => {
  const response = await fetch(`${API_BASE_URL}/market/status`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};