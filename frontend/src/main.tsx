import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";

import { PatientManagementApp } from "@/app/PatientManagementApp";
import { store } from "@/store/store";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <PatientManagementApp />
    </Provider>
  </React.StrictMode>
);
