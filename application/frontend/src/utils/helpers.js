import axios from "axios";

const config = {
  'Access-Control-Allow-Origin': '*',
  'Content-Type': 'application/json'
}

export const createUserMessage = (message) => {
  return {
    text: message,
    sender: "USER",
    messageType: "text",
    ts: new Date(),
  };
};

export const getBotResponse = async ({
  rasaServerUrl,
  sender,
  message,
  metadata = {},
}) => {
  try {
    const response = await axios({
      method: "post",
      url: rasaServerUrl,
      data: {
        sender,
        message,
        metadata,
      }
    },config);
    return response.data;
  } catch (error) {
    console.log("error occurred fetching bot response", error);
    return [];
  }
};
