export function useApi() {
  const config = useRuntimeConfig();
  const supabase = useSupabaseClient();

  async function apiFetch<T>(
    path: string,
    options: Parameters<typeof $fetch>[1] = {}
  ): Promise<T> {
    const session = await supabase.auth.getSession();
    const token = session.data.session?.access_token;

    return $fetch<T>(`${config.public.apiBase}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers ?? {}),
      },
    });
  }

  return { apiFetch };
}
