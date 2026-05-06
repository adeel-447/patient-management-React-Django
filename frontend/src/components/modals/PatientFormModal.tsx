import { type FormEvent, useState } from "react";

import { Button } from "@/components/ui/Button";
import type { Patient, PatientInput } from "@/services/patientsApi";
import { useCreatePatientMutation, useUpdatePatientMutation } from "@/services/patientsApi";

type Props = {
  initial: Patient | null;
  onClose: () => void;
  onDone: () => void;
};

export function PatientFormModal(props: Props) {
  const isEdit = props.initial !== null;
  const [createPatient, { isLoading: creating }] = useCreatePatientMutation();
  const [updatePatient, { isLoading: updating }] = useUpdatePatientMutation();

  const [firstName, setFirstName] = useState(props.initial?.first_name ?? "");
  const [lastName, setLastName] = useState(props.initial?.last_name ?? "");
  const [dob, setDob] = useState(props.initial?.date_of_birth ?? "");
  const [email, setEmail] = useState(props.initial?.email ?? "");
  const [phone, setPhone] = useState(props.initial?.phone ?? "");
  const [err, setErr] = useState<string | null>(null);

  const saving = creating || updating;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setErr(null);
    try {
      if (!firstName.trim() || !lastName.trim()) {
        throw new Error("First and last name are required.");
      }
      const normalizedEmail = email.trim().toLowerCase();
      if (normalizedEmail) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(normalizedEmail)) {
          throw new Error("Please enter a valid email address (example: ahsanaijazof@gmail.com).");
        }
      }
      const body: PatientInput = {
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        date_of_birth: dob || null,
        email: normalizedEmail,
        phone,
      };
      if (isEdit && props.initial) {
        await updatePatient({ id: props.initial.id, patch: body }).unwrap();
      } else {
        await createPatient(body).unwrap();
      }
      props.onDone();
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Save failed");
    }
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={props.onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="patient-modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <h2 id="patient-modal-title">{isEdit ? "Edit patient" : "New patient"}</h2>
          <Button variant="icon" onClick={props.onClose} aria-label="Close">
            ×
          </Button>
        </div>
        <form className="form" onSubmit={submit}>
          <div className="row">
            <label>
              First name
              <input value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
            </label>
            <label>
              Last name
              <input value={lastName} onChange={(e) => setLastName(e.target.value)} required />
            </label>
          </div>
          <label>
            Date of birth
            <input type="date" value={dob} onChange={(e) => setDob(e.target.value)} />
          </label>
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Phone
            <input value={phone} onChange={(e) => setPhone(e.target.value)} />
          </label>
          {err && <p className="error">{err}</p>}
          <div className="modal-actions">
            <Button variant="secondary" onClick={props.onClose}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={saving}>
              {saving ? "Saving…" : "Save"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
