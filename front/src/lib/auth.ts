export async function isAuthenticated() {
  const publicRouter = ["/login", "/registration"];
  const token = localStorage.getItem("auth_token");

  if (!token && !publicRouter.includes(window.location.pathname)) {
    window.location.href = "/login";
  }

  try {
    await fetch("/api/token", {
      method: "POST",
      credentials: "include",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  } catch (error) {
    if (!publicRouter.includes(window.location.pathname)) {
      window.location.href = "/login";
    }
  }
}
