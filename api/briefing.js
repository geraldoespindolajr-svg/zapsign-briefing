export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { empresa, contato, cargo, contexto } = req.body;

  if (!empresa || !contato) {
    return res.status(400).json({ error: 'Empresa e contato sao obrigatorios' });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'API key nao configurada' });
  }

  const prompt = 'Voce e um especialista em vendas enterprise B2B para uma plataforma de assinatura digital (ZapSign). Gere um briefing estrategico completo para uma reuniao de vendas com as seguintes informacoes:\n\nEmpresa: ' + empresa + '\nContato: ' + contato + '\nCargo: ' + (cargo || 'Nao informado') + '\nContexto adicional: ' + (contexto || 'Nenhum contexto adicional fornecido') + '\n\nO briefing deve incluir:\n\n1. Resumo Executivo (2-3 paragrafos sobre a empresa e oportunidade)\n2. Pontos de Dor Provaveis (liste 4-5 desafios comuns para este perfil de empresa)\n3. Proposta de Valor ZapSign (como a ZapSign resolve esses problemas)\n4. Perguntas Estrategicas (5-7 perguntas para fazer durante a reuniao)\n5. Objecoes Esperadas e Respostas (3-4 objecoes comuns com respostas preparadas)\n6. Proximos Passos Sugeridos (acoes recomendadas apos a reuniao)\n\nSeja especifico, pratico e focado em resultados de negocio.';

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-opus-4-5',
        max_tokens: 2000,
        messages: [{ role: 'user', content: prompt }]
      })
    });

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json({ error: error.error?.message || 'Erro na API' });
    }

    const data = await response.json();
    const briefing = data.content[0].text;

    return res.status(200).json({ briefing });
  } catch (error) {
    return res.status(500).json({ error: 'Erro interno: ' + error.message });
  }
}
