import { useEffect, useRef, useState } from "react";

export default function useWebSocket(host, port) {
  const ws = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const onMessageRef = useRef(null); // ref so handlers set by screens don't trigger re-renders

  useEffect(() => {
    const url = `ws://${host}:${port}`; //wss for tls
    console.log("Connecting to:", url);

    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
      setIsConnected(true);
    };

    ws.current.onmessage = (event) => {
      console.log("Received:", event.data);
      onMessageRef.current?.(event.data);  // forward to whichever screen is currently listening
    };

    ws.current.onerror = (error) => console.log("WebSocket error:", error.message || error);
    ws.current.onclose = () => {
      console.log("WebSocket closed");
      setIsConnected(false);
    };

    return () => ws.current?.close();  // cleanup on unmount or if host/port changes (wont really happen)
  }, [host, port]);

  const sendData = (data) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(data);
    } else {
      console.log("WebSocket not connected");
    }
  };;

  const setOnMessage = (fn) => {
    onMessageRef.current = fn; // screens call this to register their own message handler
  };

  return { sendData, isConnected, setOnMessage };
}