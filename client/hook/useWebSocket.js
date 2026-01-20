import { useEffect, useRef, useState } from "react";

export default function useWebSocket(host, port) {
  const ws = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    const url = `ws://${host}:${port}`;
    console.log("Connecting to:", url);

    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
    };

    ws.current.onmessage = (event) => {
      console.log("Received:", event.data);
      setLastMessage(event.data);
    };

    ws.current.onerror = (error) => {
      console.log("WebSocket error:", error.message || error);
    };

    ws.current.onclose = () => {
      console.log("WebSocket closed");
      setIsConnected(false);
    };

    return () => {
      ws.current?.close();
    };
  }, [host, port]);

  const sendData = (data) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(data);
    } else {
      console.log("WebSocket not connected");
    }
  };

  return {
    sendData,
    isConnected,
    lastMessage,
  };
}
