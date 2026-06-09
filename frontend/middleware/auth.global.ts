export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) return;

  const user = useSupabaseUser();
  const publicRoutes = ["/login", "/signup"];

  if (!user.value && !publicRoutes.includes(to.path)) {
    return navigateTo("/login");
  }
});
