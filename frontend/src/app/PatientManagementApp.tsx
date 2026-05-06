import { useState } from "react";

import { AppHeader } from "@/components/layout/AppHeader";
import { LoginForm } from "@/components/auth/LoginForm";
import { PatientTable } from "@/components/patients/PatientTable";
import { PatientToolbar } from "@/components/patients/PatientToolbar";
import { Pagination } from "@/components/ui/Pagination";
import { useAuthSession } from "@/hooks/useAuthSession";
import { usePatientModals } from "@/hooks/usePatientModals";
import { usePatientSearch } from "@/hooks/usePatientSearch";
import { AppointmentFormModal } from "@/components/modals/AppointmentFormModal";
import { DeletePatientModal } from "@/components/modals/DeletePatientModal";
import { PatientFormModal } from "@/components/modals/PatientFormModal";
import {
  useDeletePatientMutation,
  useGetPatientsQuery,
  type Patient,
} from "@/services/patientsApi";

const PAGE_SIZE = 20;

export function PatientManagementApp() {
  const { token, logout } = useAuthSession();
  const { search, setSearch } = usePatientSearch();
  const modals = usePatientModals();
  const [appointmentPatient, setAppointmentPatient] = useState<Patient | null>(null);
  const [page, setPage] = useState(1);

  const { data, isFetching, isError, refetch } = useGetPatientsQuery(
    token ? { search, page } : undefined,
    { skip: !token }
  );
  const patients = data?.results ?? [];
  const totalCount = data?.count ?? 0;
  const [deletePatient, { isLoading: deleting }] = useDeletePatientMutation();

  const handleLogout = () => {
    modals.resetSession();
    setAppointmentPatient(null);
    logout();
  };

  const header = <AppHeader showLogout={!!token} onLogout={handleLogout} />;

  if (!token) {
    return (
      <div className="page">
        {header}
        <LoginForm />
      </div>
    );
  }

  const confirmDelete = async () => {
    if (!modals.pendingDelete) return;
    modals.setDeleteError(null);
    try {
      await deletePatient(modals.pendingDelete.id).unwrap();
      modals.closeDelete();
      await refetch();
    } catch {
      modals.setDeleteError("Failed to delete patient. Please try again.");
    }
  };

  return (
    <div className="page">
      {header}
      <main>
        <PatientToolbar
          search={search}
          onSearchChange={(val) => {
            setSearch(val);
            setPage(1);
          }}
          onAddPatient={modals.openCreate}
          onRefresh={() => void refetch()}
          isFetching={isFetching}
        />

        {isError && (
          <p className="error banner">Could not load patients. Try Refresh.</p>
        )}

        <div className="card">
          <h2>Patients</h2>
          <PatientTable
            patients={patients}
            busy={isFetching}
            onEdit={modals.openEdit}
            onDeleteRequest={modals.requestDelete}
            onAddAppointment={(p) => setAppointmentPatient(p)}
          />
          <Pagination
            page={page}
            totalCount={totalCount}
            pageSize={PAGE_SIZE}
            onPageChange={setPage}
            disabled={isFetching}
          />
        </div>
      </main>

      {(modals.creating || modals.editing) && (
        <PatientFormModal
          key={modals.editing ? modals.editing.id : "new"}
          initial={modals.editing}
          onClose={modals.closeForm}
          onDone={modals.closeForm}
        />
      )}

      {modals.pendingDelete && (
        <DeletePatientModal
          patient={modals.pendingDelete}
          deleting={deleting}
          error={modals.deleteError}
          onClose={modals.closeDelete}
          onConfirm={() => void confirmDelete()}
        />
      )}

      {appointmentPatient && (
        <AppointmentFormModal
          patient={appointmentPatient}
          onClose={() => setAppointmentPatient(null)}
          onDone={() => setAppointmentPatient(null)}
        />
      )}
    </div>
  );
}
