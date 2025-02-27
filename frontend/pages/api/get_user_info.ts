import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        try {
            const { username } = req.body;

            // Simulação de recuperação de informações do usuário
            const result = {
                message: "Login successful",
                user_name: username,
                profile_picture: "/profile.jpg"
            };

            res.status(200).json(result);
        } catch {
            res.status(500).json({ message: "Falha ao recuperar informações" });
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
