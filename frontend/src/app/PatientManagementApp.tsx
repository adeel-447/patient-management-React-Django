import { AppHeader } from "@/components/layout/AppHeader";
import { LoginForm } from "@/components/auth/LoginForm";
import { PatientTable } from "@/components/patients/PatientTable";
import { PatientToolbar } from "@/components/patients/PatientToolbar";
import { useAuthSession } from "@/hooks/useAuthSession";
import { usePatientModals } from "@/hooks/usePatientModals";
import { usePatientSearch } from "@/hooks/usePatientSearch";
import { DeletePatientModal } from "@/components/modals/DeletePatientModal";
import { PatientFormModal } from "@/components/modals/PatientFormModal";
import { useDeletePatientMutation, useGetPatientsQuery } from "@/services/patientsApi";

export function PatientManagementApp() {
  const { token, logout } = useAuthSession();
  const { search, setSearch } = usePatientSearch();
  const modals = usePatientModals();

  const { data, isFetching, isError, refetch } = useGetPatientsQuery(
    token ? { search } : undefined,
    { skip: !token }
  );
  const patients = data?.results ?? [];
  const [deletePatient, { isLoading: deleting }] = useDeletePatientMutation();

  const handleLogout = () => {
    modals.resetSession();
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
          onSearchChange={setSearch}
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
    </div>
  );
}
