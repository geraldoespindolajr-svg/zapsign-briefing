export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { empresa } = req.body;

  if (!empresa || !empresa.trim()) {
    return res.status(400).json({ error: 'Nome da empresa ou site e obrigatorio' });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'API key nao configurada' });
  }

  const prompt = 'Voce e um especialista em vendas enterprise B2B para a ZapSign, plataforma de assinatura digital.' +
    ' Com base apenas no nome/site da empresa "' + empresa.trim() + '", pesquise o que voce sabe sobre essa empresa e gere um briefing estrategico completo para uma reuniao de vendas.' +
    '\n\nO briefing deve incluir:' +
    '\n\n1. **Sobre a Empresa** (segmento, porte estimado, modelo de negocio, presenca no mercado)' +
    '\n2. **Pontos de Dor Provaveis** (4-5 desafios operacionais tipicos deste perfil de empresa que a ZapSign pode resolver)' +
    '\n3. **Proposta de Valor ZapSign** (como a assinatura digital resolve os problemas especificos desta empresa)' +
    '\n4. **Perguntas Estrategicas para a Reuniao** (6-8 perguntas de discovery para fazer ao prospect)' +
    '\n5. **Objecoes Esperadas e Como Responder** (3-4 objecoes comuns com respostas preparadas)' +
    '\n6. **Proximos Passos Sugeridos** (acoes recomendadas para avancar o negocio)' +
    '\n\nSeja especifico ao perfil da empresa, pratico e focado em resultados de negocio. Se nao conhecer a empresa, baseie-se no segmento que o nome/site sugere.';

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
