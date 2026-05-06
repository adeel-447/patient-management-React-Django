import { useState } from "react";

import type { Patient } from "@/services/patientsApi";

export function usePatientModals() {
  const [editing, setEditing] = useState<Patient | null>(null);
  const [creating, setCreating] = useState(false);
  const [pendingDelete, setPendingDelete] = useState<Patient | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const openCreate = () => {
    setEditing(null);
    setCreating(true);
  };

  const openEdit = (patient: Patient) => {
    setCreating(false);
    setEditing(patient);
  };

  const closeForm = () => {
    setCreating(false);
    setEditing(null);
  };

  const requestDelete = (patient: Patient) => {
    setDeleteError(null);
    setPendingDelete(patient);
  };

  const closeDelete = () => {
    setPendingDelete(null);
  };

  const resetSession = () => {
    closeForm();
    setPendingDelete(null);
    setDeleteError(null);
  };

  return {
    editing,
    creating,
    pendingDelete,
    deleteError,
    setDeleteError,
    openCreate,
    openEdit,
    closeForm,
    requestDelete,
    closeDelete,
    resetSession,
  };
}
