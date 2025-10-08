module.exports = {
  apps: [
    {
      name: 'taveirabot-telegram',
      script: 'main.py',
      // Aponta para o interpretador Python dentro do seu ambiente virtual
      interpreter: '.venv/bin/python',
      // Garante que o bot inicie no diretório correto para encontrar o .env
      cwd: '/home/taveira/repositories/taveirabot-telegram',
      // Reinicia o app automaticamente em caso de falha
      autorestart: true,
      // Não monitora mudanças nos arquivos em produção
      watch: false,
      // Limita as reinicializações em caso de falhas constantes
      max_restarts: 5,
      min_uptime: '1m',
      // Reinicia o app se ele usar mais de 150MB de RAM
      max_memory_restart: "150M",
      // Arquivos de log
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      error_file: 'logs/error.log',
      out_file: 'logs/out.log',
      merge_logs: true,
    },
  ],
};
