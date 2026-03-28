import useWebSocket from "@/hook/useWebSocket";
import { createContext } from "react";

export const UserContext = createContext<{
  webSocket: ReturnType<typeof useWebSocket>;
  userId: string | null;
  setUserId: React.Dispatch<React.SetStateAction<string | null>>;
  room_number: string | null;
  setRoom_number: React.Dispatch<React.SetStateAction<string | null>>;
} | null>(null);

export const MarkerContext = createContext<{
  //Here I will store the latitude and longitude of the marker that the user has chosen to place on the map, so it can be sent to the server when the user chooses a mark type
  Mark_latitude: number | null;
  setMark_latitude: React.Dispatch<React.SetStateAction<number | null>>;
  Mark_longitude: number | null;
  setMark_longitude: React.Dispatch<React.SetStateAction<number | null>>;
  ChosenMark: string | null; // path of the chosen mark image
  setChosenMark: React.Dispatch<React.SetStateAction<string | null>>;
} | null>(null);

