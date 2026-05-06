import { Button } from "@/components/ui/Button";
import { formatWhen } from "@/utils/formatWhen";
import type { Patient } from "@/services/patientsApi";

type Props = {
  patients: Patient[];
  busy: boolean;
  onEdit: (p: Patient) => void;
  onDeleteRequest: (p: Patient) => void;
  onAddAppointment: (p: Patient) => void;
};

export function PatientTable(props: Props) {
  if (props.busy && props.patients.length === 0) {
    return <p className="muted">Loading…</p>;
  }
  if (props.patients.length === 0) {
    return <p className="muted">No patients yet. Add one to get started.</p>;
  }

  return (
    <div className="table-wrap">
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>DOB</th>
            <th>Contact</th>
            <th>Appointments</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {props.patients.map((p) => (
            <tr key={p.id}>
              <td>
                <strong>
                  {p.last_name}, {p.first_name}
                </strong>
              </td>
              <td>{p.date_of_birth ?? "—"}</td>
              <td>
                <div className="stack">
                  {p.email && <span>{p.email}</span>}
                  {p.phone && <span>{p.phone}</span>}
                  {!p.email && !p.phone && <span className="muted">—</span>}
                </div>
              </td>
              <td>
                {p.appointments.length === 0 ? (
                  <span className="muted">None</span>
                ) : (
                  <ul className="appt-list">
                    {p.appointments.map((a) => (
                      <li key={a.id}>
                        {formatWhen(a.scheduled_at)}
                        {a.clinician_names.length > 0 && (
                          <span className="muted small">
                            {" "}
                            · {a.clinician_names.join(", ")}
                          </span>
                        )}
                      </li>
                    ))}
                  </ul>
                )}
              </td>
              <td className="actions">
                <Button variant="link" onClick={() => props.onAddAppointment(p)}>
                  + Appt
                </Button>
                <Button variant="link" onClick={() => props.onEdit(p)}>
                  Edit
                </Button>
                <Button variant="link" danger onClick={() => props.onDeleteRequest(p)}>
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
