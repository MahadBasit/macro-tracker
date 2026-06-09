export default defineNuxtRouteMiddleware((to) => {
  const user = useSupabaseUser();
  const publicRoutes = ["/login", "/signup"];

  if (!user.value && !publicRoutes.includes(to.path)) {
    return navigateTo("/login");
  }
});
