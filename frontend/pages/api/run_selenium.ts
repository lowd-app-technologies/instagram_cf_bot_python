import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        try {
            // Simulação de execução do Selenium
            const usuarios_adicionados = 10;

            res.status(200).json({
                success: true,
                usuarios_adicionados: usuarios_adicionados
            });
        } catch {
            res.status(500).json({ message: "Falha ao executar Selenium" });
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
