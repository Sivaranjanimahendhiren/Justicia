import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1";

export async function sendQuery(query, sessionId = null) {
  const response = await axios.post(`${BASE_URL}/chat`, {
    query,
    session_id: sessionId,
  });
  return response.data;
}
