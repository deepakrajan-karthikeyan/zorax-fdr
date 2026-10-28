const SUPABASE_HOST = process.env.SUPABASE_DB_HOST || "db.yzlkhilnnextpmrkdzvk.supabase.co";
const SUPABASE_PORT = process.env.SUPABASE_DB_PORT || "5432";
const SUPABASE_NAME = process.env.SUPABASE_DB_NAME || "postgres";
const SUPABASE_USER = process.env.SUPABASE_DB_USER || "postgres";

function getDatabaseConfig() {
  const password = process.env.SUPABASE_DB_PASSWORD;
  return {
    host: SUPABASE_HOST,
    port: Number(SUPABASE_PORT),
    database: SUPABASE_NAME,
    user: SUPABASE_USER,
    configured: Boolean(password),
    connectionString: password
      ? `postgresql://${encodeURIComponent(SUPABASE_USER)}:${encodeURIComponent(password)}@${SUPABASE_HOST}:${SUPABASE_PORT}/${SUPABASE_NAME}`
      : null
  };
}

module.exports = { getDatabaseConfig };
