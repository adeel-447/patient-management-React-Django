import { type FormEvent, useState } from "react";

import { Button } from "@/components/ui/Button";
import {
  useCreateAppointmentMutation,
  useGetCliniciansQuery,
} from "@/services/patientsApi";
import type { Patient } from "@/services/patientsApi";

type Props = {
  patient: Patient;
  onClose: () => void;
  onDone: () => void;
};

export function AppointmentFormModal(props: Props) {
  const [createAppointment, { isLoading }] = useCreateAppointmentMutation();
  const { data: clinicians = [], isLoading: loadingClinicians } =
    useGetCliniciansQuery();

  const [scheduledAt, setScheduledAt] = useState("");
  const [notes, setNotes] = useState("");
  const [selectedClinicians, setSelectedClinicians] = useState<number[]>([]);
  const [err, setErr] = useState<string | null>(null);

  const toggleClinician = (id: number) => {
    setSelectedClinicians((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    );
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setErr(null);
    try {
      if (!scheduledAt) {
        throw new Error("Scheduled date/time is required.");
      }
      if (selectedClinicians.length === 0) {
        throw new Error("Please select at least one clinician.");
      }
      await createAppointment({
        patient: props.patient.id,
        scheduled_at: new Date(scheduledAt).toISOString(),
        notes,
        clinicians: selectedClinicians,
      }).unwrap();
      props.onDone();
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Failed to create appointment.");
    }
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={props.onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="appt-modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <h2 id="appt-modal-title">
            Add appointment for {props.patient.first_name} {props.patient.last_name}
          </h2>
          <Button variant="icon" onClick={props.onClose} aria-label="Close">
            ×
          </Button>
        </div>
        <form className="form" onSubmit={submit}>
          <label>
            Scheduled date &amp; time
            <input
              type="datetime-local"
              value={scheduledAt}
              onChange={(e) => setScheduledAt(e.target.value)}
              required
            />
          </label>
          <label>
            Notes
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              placeholder="Optional notes..."
            />
          </label>
          <fieldset className="clinician-fieldset">
            <legend>Clinicians (select one or more)</legend>
            {loadingClinicians && <p className="muted">Loading clinicians…</p>}
            {clinicians.length === 0 && !loadingClinicians && (
              <p className="muted">No clinicians found for your clinic.</p>
            )}
            <div className="checkbox-group">
              {clinicians.map((c) => (
                <label key={c.id} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={selectedClinicians.includes(c.id)}
                    onChange={() => toggleClinician(c.id)}
                  />
                  {c.first_name} {c.last_name}
                </label>
              ))}
            </div>
          </fieldset>
          {err && <p className="error">{err}</p>}
          <div className="modal-actions">
            <Button variant="secondary" onClick={props.onClose}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={isLoading}>
              {isLoading ? "Creating…" : "Create appointment"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
