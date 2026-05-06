import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import { getApiBase } from "@/services/apiBase";
import { setCredentials } from "@/store/authSlice";

type TokenResponse = {
  access: string;
  refresh: string;
};

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: getApiBase(),
    prepareHeaders: (headers) => {
      headers.set("Content-Type", "application/json");
      return headers;
    },
  }),
  endpoints: (builder) => ({
    login: builder.mutation<TokenResponse, { username: string; password: string }>({
      query: (body) => ({
        url: "auth/login/",
        method: "POST",
        body,
      }),
      async onQueryStarted(_arg, { dispatch, queryFulfilled }) {
        const { data } = await queryFulfilled;
        dispatch(setCredentials(data.access));
      },
    }),
  }),
});

export const { useLoginMutation } = authApi;
