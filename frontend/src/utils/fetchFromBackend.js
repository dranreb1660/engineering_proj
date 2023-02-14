import axios from "axios";

const BASE_URL = "http://localhost:5100";

export const fetchInputs = async () => {
  const { data } = await axios.get(`${BASE_URL}/get_inputs`);
  return data;
};

export const fetchPrediction = async (payload) => {
  const config = {
    headers: {
      "Content-type": "application/json",
    },
  };

  const { data } = await axios.post(
    `${BASE_URL}/auto_predict`,
    payload,
    config
  );
  return data;
};
