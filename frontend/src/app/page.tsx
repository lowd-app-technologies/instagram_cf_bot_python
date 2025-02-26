"use client";

import { useState } from "react";
import { Progress } from "@/components/ui/progress"; 

export default function Home() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [progress, setProgress] = useState(0);
  const [userInfo, setUserInfo] = useState(null); 
  const [addingFollowers, setAddingFollowers] = useState(false); 
  const [followersProgress, setFollowersProgress] = useState(0); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");


    const timer = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(timer);
          return 100;
        }
        return Math.min(oldProgress + 10, 100);
      });
    }, 500);

    try {
      const response = await fetch("http://127.0.0.1:8000/get_user_info/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      setLoading(false);

      if (data.message) {
        setIsSuccess(true);
        setUserInfo({
          name: data.user_name,
          profilePicture: data.profile_picture,
        });
        startAddingFollowers(); 
      } else if (data.error) {
        setIsSuccess(false);
        setMessage(data.error);
      }
    } catch (error) {
      setLoading(false);
      setIsSuccess(false);
      setMessage("Ocorreu um erro ao se conectar ao servidor.");
    }
  };


  const startAddingFollowers = async () => {
    setAddingFollowers(true);
    setFollowersProgress(0);


    const timer = setInterval(() => {
      setFollowersProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(timer);
          return 100;
        }
        return Math.min(oldProgress + 10, 100);
      });
    }, 500);

    try {
      const response = await fetch("http://127.0.0.1:8000/run_selenium/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (data.usuarios_adicionados) {
        setMessage(`Adicionados ${data.usuarios_adicionados} seguidores ao Close Friends!`);
      } else {
        setMessage("Erro ao adicionar seguidores.");
      }
    } catch (error) {
      setMessage("Erro ao conectar para adicionar seguidores.");
    } finally {
      setAddingFollowers(false);
    }
  };

  return (
    <div className="flex flex-col items-center p-6 bg-gray-50 min-h-screen justify-center">
      <h1 className="text-3xl font-bold text-center mb-6">
        Adicionar Close Friends
      </h1>

      {userInfo ? (
        <div className="text-center mb-6">
          <img
            src={`http://127.0.0.1:8000${userInfo.profilePicture}`} 
            alt="Foto de perfil"
            className="w-32 h-32 rounded-full mx-auto mb-4"
          />
          <h2 className="text-xl font-semibold">Bem-vindo, {userInfo.name}!</h2>
          <p className="text-gray-600 mt-2">
            Estamos trabalhando em tudo, aguarde alguns instantes...
          </p>
          {loading && <Progress value={progress} className="w-full mt-4" />}
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6 w-full max-w-md">
          <input
            type="text"
            placeholder="Usuário"
            className="border p-3 w-full rounded-md shadow-sm focus:ring-2 focus:ring-blue-500"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Senha"
            className="border p-3 w-full rounded-md shadow-sm focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg w-full hover:bg-blue-700 transition duration-200"
            disabled={loading}
          >
            {loading ? "Processando..." : "Iniciar"}
          </button>

          {loading && <Progress value={progress} className="w-full mt-4" />}
        </form>
      )}

      {addingFollowers && <Progress value={followersProgress} className="w-full mt-4" />}

      {message && (
        <p
          className={`mt-4 p-4 rounded-lg w-full text-center font-semibold ${
            isSuccess
              ? "bg-green-100 text-green-600"
              : "bg-red-100 text-red-600"
          }`}
        >
          {message}
        </p>
      )}
    </div>
  );
}
