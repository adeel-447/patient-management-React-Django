import { useState } from "react";

export function usePatientSearch() {
  const [search, setSearch] = useState("");
  return { search, setSearch };
}
