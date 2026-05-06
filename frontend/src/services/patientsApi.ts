import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import { getApiBase } from "@/services/apiBase";

type AuthStateSlice = { auth: { accessToken: string | null } };

export type Patient = {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string | null;
  email: string;
  phone: string;
  created_at: string;
  updated_at: string;
  appointments: {
    id: number;
    scheduled_at: string;
    notes: string;
    clinician_names: string[];
  }[];
};

export type PatientInput = {
  first_name: string;
  last_name: string;
  date_of_birth: string | null;
  email: string;
  phone: string;
};

export type PatientListResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Patient[];
};

export const patientsApi = createApi({
  reducerPath: "patientsApi",
  baseQuery: fetchBaseQuery({
    baseUrl: getApiBase(),
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as AuthStateSlice).auth.accessToken;
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      headers.set("Content-Type", "application/json");
      return headers;
    },
  }),
  tagTypes: ["Patient"],
  endpoints: (builder) => ({
    getPatients: builder.query<PatientListResponse, { page?: number; search?: string } | void>({
      query: (params) => {
        const query = new URLSearchParams();
        if (params?.page) query.set("page", String(params.page));
        if (params?.search) query.set("search", params.search);
        const suffix = query.toString();
        return suffix ? `patients/?${suffix}` : "patients/";
      },
      providesTags: (result) =>
        result?.results
          ? [
              ...result.results.map((p) => ({ type: "Patient" as const, id: p.id })),
              { type: "Patient", id: "LIST" },
            ]
          : [{ type: "Patient", id: "LIST" }],
    }),
    createPatient: builder.mutation<Patient, PatientInput>({
      query: (body) => ({ url: "patients/", method: "POST", body }),
      invalidatesTags: [{ type: "Patient", id: "LIST" }],
    }),
    updatePatient: builder.mutation<
      Patient,
      { id: number; patch: Partial<PatientInput> }
    >({
      query: ({ id, patch }) => ({
        url: `patients/${id}/`,
        method: "PATCH",
        body: patch,
      }),
      invalidatesTags: (_r, _e, { id }) => [
        { type: "Patient", id },
        { type: "Patient", id: "LIST" },
      ],
    }),
    deletePatient: builder.mutation<void, number>({
      query: (id) => ({ url: `patients/${id}/`, method: "DELETE" }),
      invalidatesTags: (_r, _e, id) => [
        { type: "Patient", id },
        { type: "Patient", id: "LIST" },
      ],
    }),
  }),
});

export const {
  useGetPatientsQuery,
  useCreatePatientMutation,
  useUpdatePatientMutation,
  useDeletePatientMutation,
} = patientsApi;
