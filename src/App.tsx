/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect } from 'react';

type SexeType = 'femme' | 'homme' | 'autre' | '';

export default function App() {
  // Form fields
  const [nom, setNom] = useState('Dupont');
  const [prenom, setPrenom] = useState('Camille');
  const [age, setAge] = useState('34');
  const [sexe, setSexe] = useState<SexeType>('femme');

  // Field validation errors
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  // Camera and capture state
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [flashOn, setFlashOn] = useState(false);
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('user');
  const [cameraStream, setCameraStream] = useState<MediaStream | null>(null);
  const [cameraError, setCameraError] = useState<string | null>(null);

  // Analysis state
  const [isSending, setIsSending] = useState(false);
  const [isDone, setIsDone] = useState(false);
  const [resultText, setResultText] = useState<string | null>(null);
  const [resultTime, setResultTime] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<{ type: 'noConnection' | 'server' | 'timeout'; text: string; icon: string } | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const captureCardRef = useRef<HTMLDivElement>(null);
  const previewCardRef = useRef<HTMLDivElement>(null);
  const loadingCardRef = useRef<HTMLDivElement>(null);
  const resultsCardRef = useRef<HTMLDivElement>(null);

  // Initialize camera with webcam if possible
  useEffect(() => {
    let stream: MediaStream | null = null;
    async function initCamera() {
      try {
        setCameraError(null);
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: facingMode, width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: false,
        });
        setCameraStream(stream);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.warn('Camera not available or permission denied:', err);
        setCameraError("L'accès à la caméra est nécessaire pour photographier vos yeux.");
      }
    }

    initCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [facingMode]);

  const handleCapture = () => {
    if (isCapturing || isSending) return;
    setIsCapturing(true);

    setTimeout(() => {
      // Capture frame from video or fallback canvas
      if (videoRef.current && videoRef.current.videoWidth > 0) {
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(videoRef.current, 0, 0);
          setPhotoUrl(canvas.toDataURL('image/png'));
        }
      } else {
        // Fallback realistic eye screening sample image
        setPhotoUrl('https://lh3.googleusercontent.com/aida-public/AB6AXuBKtFQAccLYPPdhGA0NM2-hUSAxvitbJe7gYZG3tH3CpPrtw4xzOISIUYXxPFJnF6k_e7kjez_E6pwP7YVdgL__8kvU_6-MOwebZku_p_TwJiymeMlh3VBXxqwmgA4aQ37Q4qWHYarjxOOr-fPQSgJpqzWDyny47YofL2zLnV6zdbZhyAIwFGe5g8Ns_45dWn32WjawxiEg7oc7pQxVU1vmNr00_ikMd_H6uEu9FIxv');
      }

      setIsCapturing(false);
      setErrorMessage(null);
      setIsDone(false);

      setTimeout(() => {
        previewCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 100);
    }, 200);
  };

  const handleRetake = () => {
    setPhotoUrl(null);
    setIsDone(false);
    setErrorMessage(null);
    captureCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const validate = () => {
    const newErrors: { [key: string]: string } = {};
    if (!nom.trim()) newErrors.nom = 'Ce champ est obligatoire';
    else if (nom.trim().length > 60) newErrors.nom = '60 caractères maximum';

    if (!prenom.trim()) newErrors.prenom = 'Ce champ est obligatoire';
    else if (prenom.trim().length > 60) newErrors.prenom = '60 caractères maximum';

    const ageNum = parseInt(age, 10);
    if (!age || isNaN(ageNum) || ageNum < 1 || ageNum > 120) {
      newErrors.age = 'Entrez un âge valide (de 1 à 120)';
    }

    if (!sexe) {
      newErrors.sexe = 'Veuillez sélectionner une option';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAnalyze = () => {
    if (!validate()) {
      return;
    }

    setResultText(null);
    setErrorMessage(null);
    setIsSending(true);
    setIsDone(false);

    loadingCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Simulate screening API response (or live API)
    setTimeout(() => {
      setIsSending(false);
      setIsDone(true);
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, '0');
      const mins = String(now.getMinutes()).padStart(2, '0');
      setResultTime(`Aujourd'hui à ${hours}:${mins}`);
      setResultText(
        "L'analyse simultanée de vos deux yeux confirme une excellente homogénéité globale. La clarté sclérale, la coloration conjonctivale ainsi que les reflets micro-vasculaires se situent dans les normes physiologiques idéales, sans signe d'ictère, d'anémie ou de fatigue excessive détecté."
      );

      setTimeout(() => {
        resultsCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    }, 2800);
  };

  return (
    <div className="min-h-screen bg-[#FFF8F5] text-[#1D1B19] flex flex-col items-center">
      {/* Fixed Header */}
      <header className="fixed top-0 inset-x-0 h-16 bg-[#FFF8F5]/80 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-50 flex items-center justify-center">
        <div className="w-full max-w-[480px] px-5 flex items-center justify-between">
          <span className="font-bold text-[18px] tracking-tight text-[#1D1B19]">Dépiste Retino</span>
          <span className="text-[11px] font-semibold tracking-wide uppercase px-2 py-0.5 rounded-full bg-[#E5AD5C]/20 text-[#815508]">
            Flutter App
          </span>
        </div>
      </header>

      {/* Main Container */}
      <main className="w-full max-w-[480px] pt-20 pb-12 px-5 flex flex-col space-y-6">
        {/* 1. Introduction Section */}
        <section className="flex flex-col space-y-2 pt-2">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#BFEAC5] text-[#446B4D] text-[12px] font-bold">
              <span className="material-symbols-outlined text-[15px] fill-1">spa</span>
              Dépistage bienveillant
            </span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#EDE7E4] text-[#53433F] text-[12px] font-bold">
              <span className="w-1.5 h-1.5 rounded-full bg-[#406749]"></span>
              IA Santé v2.4
            </span>
          </div>
          <h1 className="text-[26px] leading-[34px] font-bold tracking-tight text-[#1D1B19]">
            Un petit contrôle de vos yeux, en quelques secondes.
          </h1>
          <p className="text-[15px] leading-[23px] text-[#53433F]">
            Positionnez confortablement votre regard. Nous veillons sur la clarté et la vitalité de vos yeux en une seule prise bienveillante.
          </p>
        </section>

        {/* 2. Vos informations Card */}
        <section className="bg-white rounded-[32px] p-5 shadow-[0px_4px_20px_-2px_rgba(61,58,56,0.06)] flex flex-col space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-[#FFDBD1] flex items-center justify-center text-[#8D4D3B]">
                <span className="material-symbols-outlined text-[18px]">badge</span>
              </div>
              <div>
                <h2 className="text-[16px] leading-[22px] font-bold text-[#1D1B19]">Vos informations</h2>
                <p className="text-[13px] leading-[19px] text-[#53433F]">Nécessaire pour calibrer l'analyse</p>
              </div>
            </div>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-[#F3EDE9] text-[#53433F] text-[12px] font-bold">
              <span className="material-symbols-outlined text-[14px] text-[#406749]">lock</span>
              Confidentiel
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            {/* Nom */}
            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] font-semibold text-[#1D1B19]">Nom</label>
              <input
                type="text"
                value={nom}
                onChange={(e) => {
                  setNom(e.target.value);
                  if (errors.nom) setErrors({ ...errors, nom: '' });
                  if (isDone) setIsDone(false);
                }}
                placeholder="Dupont"
                className={`w-full min-h-[52px] px-4 rounded-full bg-[#F9F2EF] border ${
                  errors.nom ? 'border-[#BA1A1A] border-[1.5px]' : 'border-[#EDE7E4]/60'
                } text-[#1D1B19] placeholder:text-[#53433F]/60 text-[15px] focus:outline-none focus:ring-2 focus:ring-[#8D4D3B]/30 transition-all`}
              />
              {errors.nom && <span className="text-[13px] text-[#BA1A1A] pl-2">{errors.nom}</span>}
            </div>

            {/* Prénom */}
            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] font-semibold text-[#1D1B19]">Prénom</label>
              <input
                type="text"
                value={prenom}
                onChange={(e) => {
                  setPrenom(e.target.value);
                  if (errors.prenom) setErrors({ ...errors, prenom: '' });
                  if (isDone) setIsDone(false);
                }}
                placeholder="Camille"
                className={`w-full min-h-[52px] px-4 rounded-full bg-[#F9F2EF] border ${
                  errors.prenom ? 'border-[#BA1A1A] border-[1.5px]' : 'border-[#EDE7E4]/60'
                } text-[#1D1B19] placeholder:text-[#53433F]/60 text-[15px] focus:outline-none focus:ring-2 focus:ring-[#8D4D3B]/30 transition-all`}
              />
              {errors.prenom && <span className="text-[13px] text-[#BA1A1A] pl-2">{errors.prenom}</span>}
            </div>

            {/* Âge */}
            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] font-semibold text-[#1D1B19]">Âge</label>
              <input
                type="number"
                value={age}
                onChange={(e) => {
                  setAge(e.target.value);
                  if (errors.age) setErrors({ ...errors, age: '' });
                  if (isDone) setIsDone(false);
                }}
                placeholder="34 ans"
                min="1"
                max="120"
                className={`w-full min-h-[52px] px-4 rounded-full bg-[#F9F2EF] border ${
                  errors.age ? 'border-[#BA1A1A] border-[1.5px]' : 'border-[#EDE7E4]/60'
                } text-[#1D1B19] placeholder:text-[#53433F]/60 text-[15px] focus:outline-none focus:ring-2 focus:ring-[#8D4D3B]/30 transition-all`}
              />
              {errors.age && <span className="text-[13px] text-[#BA1A1A] pl-2">{errors.age}</span>}
            </div>

            {/* Sexe */}
            <div className="flex flex-col gap-1.5">
              <label className="text-[12px] font-semibold text-[#1D1B19]">Sexe</label>
              <div className="relative flex items-center">
                <select
                  value={sexe}
                  onChange={(e) => {
                    setSexe(e.target.value as SexeType);
                    if (errors.sexe) setErrors({ ...errors, sexe: '' });
                    if (isDone) setIsDone(false);
                  }}
                  className={`w-full min-h-[52px] px-4 pr-10 rounded-full bg-[#F9F2EF] border ${
                    errors.sexe ? 'border-[#BA1A1A] border-[1.5px]' : 'border-[#EDE7E4]/60'
                  } text-[#1D1B19] text-[15px] focus:outline-none focus:ring-2 focus:ring-[#8D4D3B]/30 transition-all appearance-none cursor-pointer`}
                >
                  <option value="" disabled>Sélectionner...</option>
                  <option value="femme">Femme</option>
                  <option value="homme">Homme</option>
                  <option value="autre">Autre / Non précisé</option>
                </select>
                <span className="material-symbols-outlined text-[20px] text-[#53433F] absolute right-3 pointer-events-none">
                  expand_more
                </span>
              </div>
              {errors.sexe && <span className="text-[13px] text-[#BA1A1A] pl-2">{errors.sexe}</span>}
            </div>
          </div>
        </section>

        {/* 3. Carte de capture appareil photo */}
        <section
          ref={captureCardRef}
          className="bg-white rounded-[32px] p-5 shadow-[0px_4px_20px_-2px_rgba(61,58,56,0.06)] flex flex-col items-center relative overflow-hidden transition-all duration-300"
        >
          {/* Card Header */}
          <div className="w-full flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-[#FFDBD1] flex items-center justify-center text-[#8D4D3B]">
                <span className="material-symbols-outlined text-[18px]">photo_camera</span>
              </div>
              <span className="text-[14px] font-semibold text-[#1D1B19]">Viseur guidé simultané</span>
            </div>
            <div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-[#F3EDE9] text-[#53433F] text-[12px] font-bold">
              <span className="material-symbols-outlined text-[15px] text-[#815508]">wb_sunny</span>
              <span>Lumière naturelle</span>
            </div>
          </div>

          {/* Viseur oculaire avec double repère */}
          <div className="relative w-full aspect-[4/3] rounded-2xl bg-[#F3EDE9] overflow-hidden flex items-center justify-center shadow-inner">
            {/* Live video or fallback */}
            {cameraStream ? (
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="absolute inset-0 w-full h-full object-cover"
              />
            ) : (
              <div className="absolute inset-0 bg-gradient-to-b from-[#DFD9D6]/40 via-[#F3EDE9]/20 to-[#DFD9D6]/50"></div>
            )}

            {/* Flash & Flip buttons */}
            <div className="absolute top-3 left-3 z-20">
              <button
                onClick={() => setFlashOn(!flashOn)}
                title={flashOn ? 'Désactiver le flash' : 'Activer le flash'}
                aria-label={flashOn ? 'Désactiver le flash' : 'Activer le flash'}
                className="w-11 h-11 rounded-full bg-[#33302E]/85 backdrop-blur-md text-[#F6EFEC] flex items-center justify-center shadow-md active:scale-95 transition-transform"
              >
                <span className="material-symbols-outlined text-[20px]">
                  {flashOn ? 'flash_on' : 'flash_off'}
                </span>
              </button>
            </div>

            <div className="absolute top-3 right-3 z-20">
              <button
                onClick={() => setFacingMode(facingMode === 'user' ? 'environment' : 'user')}
                title="Changer de caméra"
                aria-label="Changer de caméra"
                className="w-11 h-11 rounded-full bg-[#33302E]/85 backdrop-blur-md text-[#F6EFEC] flex items-center justify-center shadow-md active:scale-95 transition-transform"
              >
                <span className="material-symbols-outlined text-[20px]">cameraswitch</span>
              </button>
            </div>

            {/* Dual-eye guide overlay with SVG */}
            <div className="relative w-[88%] h-36 rounded-full flex items-center justify-center shadow-[0_0_0_9999px_rgba(29,27,25,0.22)] pointer-events-none">
              <svg className="absolute inset-0 w-full h-full pointer-events-none" fill="none" viewBox="0 0 290 144">
                {/* Grand masque englobant les deux yeux avec pulsation */}
                <rect
                  className="animate-pulse"
                  x="6"
                  y="14"
                  width="278"
                  height="116"
                  rx="58"
                  stroke="#F4A38C"
                  strokeWidth="2.5"
                  strokeDasharray="6 6"
                  strokeLinecap="round"
                />
                {/* Oeil gauche */}
                <circle cx="82" cy="72" r="32" stroke="#FFFFFF" strokeOpacity="0.85" strokeWidth="1.5" strokeDasharray="4 4" />
                <circle cx="82" cy="72" r="12" stroke="#FFFFFF" strokeOpacity="0.9" strokeWidth="1.5" />
                <circle cx="82" cy="72" r="2.5" fill="#FFFFFF" />
                {/* Oeil droit */}
                <circle cx="208" cy="72" r="32" stroke="#FFFFFF" strokeOpacity="0.85" strokeWidth="1.5" strokeDasharray="4 4" />
                <circle cx="208" cy="72" r="12" stroke="#FFFFFF" strokeOpacity="0.9" strokeWidth="1.5" />
                <circle cx="208" cy="72" r="2.5" fill="#FFFFFF" />
                {/* Repère pont de nez */}
                <path d="M 145 60 L 145 84" stroke="#FFFFFF" strokeOpacity="0.6" strokeWidth="1.5" strokeLinecap="round" />
                <path d="M 141 72 L 149 72" stroke="#FFFFFF" strokeOpacity="0.6" strokeWidth="1.5" strokeLinecap="round" />
              </svg>

              <div className="flex flex-col items-center justify-center text-center px-4 py-2 z-10 backdrop-blur-[2px]">
                <span className="material-symbols-outlined text-[#FFF8F5] text-[26px] drop-shadow-md">visibility</span>
                <span className="text-[12px] font-bold text-[#FFF8F5] tracking-wide drop-shadow-sm mt-0.5">
                  Positionnez vos deux yeux dans le cadre
                </span>
              </div>
            </div>
          </div>

          {/* Instruction d'accompagnement */}
          <div className="flex items-center gap-2.5 mt-3.5 px-3 py-2 rounded-full bg-[#F9F2EF] w-full">
            <div className="w-7 h-7 rounded-full bg-[#FFDDB3] flex items-center justify-center shrink-0">
              <span className="material-symbols-outlined text-[#291800] text-[16px]">light_mode</span>
            </div>
            <p className="text-[13px] text-[#53433F]">
              Placez vos yeux face à l'objectif, à environ 30 cm, dans un endroit bien éclairé.
            </p>
          </div>

          {/* Shutter button */}
          <div className="flex flex-col items-center justify-center mt-5 mb-2 w-full">
            <div className="relative flex items-center justify-center">
              <span className="absolute w-24 h-24 rounded-full bg-[#F4A38C]/40 animate-ping opacity-75 pointer-events-none"></span>
              <button
                onClick={handleCapture}
                disabled={isCapturing || isSending}
                aria-label="Prendre la photo"
                className="relative z-10 w-20 h-20 rounded-full bg-[#F4A38C] text-[#713726] shadow-[0px_8px_24px_rgba(244,163,140,0.55)] active:scale-95 transition-all flex items-center justify-center group focus:outline-none disabled:opacity-50"
              >
                <div className="w-16 h-16 rounded-full bg-white flex items-center justify-center shadow-inner group-active:bg-[#FFDBD1]">
                  {isCapturing ? (
                    <div className="w-7 h-7 border-3 border-[#8D4D3B] border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <span className="material-symbols-outlined text-[#8D4D3B] text-[32px] group-hover:scale-110 transition-transform">
                      photo_camera
                    </span>
                  )}
                </div>
              </button>
            </div>
            <span className="text-[12px] font-medium text-[#53433F] mt-2">Appuyer pour capturer</span>
          </div>
        </section>

        {/* 4. Carte « Cliché instantané » (visible si photo prise) */}
        {photoUrl && (
          <section
            ref={previewCardRef}
            className="bg-white rounded-[32px] p-5 shadow-[0px_4px_20px_-2px_rgba(61,58,56,0.06)] flex flex-col space-y-4 transition-all"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-[#406749]"></span>
                <span className="text-[18px] font-semibold text-[#1D1B19]">Cliché instantané</span>
              </div>
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-[#C1EDC8] text-[#284F33] text-[12px] font-bold">
                <span className="material-symbols-outlined text-[14px]">check_circle</span>
                Prêt pour l'analyse
              </span>
            </div>

            {/* Photo preview with bottom gradient */}
            <div className="relative w-full aspect-[16/10] max-h-72 rounded-2xl overflow-hidden bg-[#F3EDE9] shadow-md">
              <img src={photoUrl} alt="Aperçu des deux yeux" className="w-full h-full object-cover" />
              <div className="absolute inset-x-0 bottom-0 h-6 bg-gradient-to-t from-[#33302E]/80 via-[#33302E]/30 to-transparent pointer-events-none"></div>
            </div>

            {/* Actions */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              <button
                onClick={handleRetake}
                disabled={isSending}
                className="w-full min-h-[56px] rounded-full bg-[#EDE7E4] hover:bg-[#DFD9D6] active:scale-[0.98] transition-all flex items-center justify-center gap-2 text-[#1D1B19] text-[16px] font-semibold disabled:opacity-50"
              >
                <span className="material-symbols-outlined text-[20px]">replay</span>
                <span>Reprendre</span>
              </button>

              <button
                onClick={handleAnalyze}
                disabled={isSending || isDone}
                className="w-full min-h-[56px] rounded-full bg-[#F4A38C] text-[#713726] shadow-[0px_6px_20px_0px_rgba(244,163,140,0.4)] hover:brightness-105 active:scale-[0.98] transition-all flex items-center justify-center gap-2 text-[16px] font-bold disabled:opacity-60"
              >
                {isSending ? (
                  <>
                    <span className="material-symbols-outlined text-[20px] animate-spin">sync</span>
                    <span>Analyse...</span>
                  </>
                ) : isDone ? (
                  <>
                    <span>Analyse terminée</span>
                    <span className="material-symbols-outlined text-[20px]">done</span>
                  </>
                ) : (
                  <>
                    <span>Analyser</span>
                    <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
                  </>
                )}
              </button>
            </div>
          </section>
        )}

        {/* 5. Carte de chargement (visible pendant l'envoi) */}
        {isSending && (
          <section
            ref={loadingCardRef}
            className="bg-white rounded-[32px] p-5 shadow-[0px_4px_20px_-2px_rgba(61,58,56,0.06)] flex flex-col items-center text-center space-y-4"
          >
            <div className="flex items-center justify-center gap-2.5 w-full py-1">
              <span className="w-2.5 h-2.5 rounded-full bg-[#8D4D3B] animate-pulse"></span>
              <span className="text-[18px] font-semibold text-[#1D1B19]">Analyse en cours…</span>
            </div>

            <div className="w-full bg-[#F9F2EF] rounded-2xl p-4 flex flex-col space-y-3 text-left">
              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-full bg-[#BFEAC5] flex items-center justify-center shrink-0 mt-0.5">
                  <span className="material-symbols-outlined text-[#406749] text-[16px]">check</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-[14px] font-semibold text-[#1D1B19]">Clarté sclérale bilatérale</span>
                  <span className="text-[13px] text-[#53433F]">
                    Recherche d'indices pigmentaires ou jaunâtres sur les deux yeux.
                  </span>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-full bg-[#FFDBD1] flex items-center justify-center shrink-0 mt-0.5 animate-pulse">
                  <span className="material-symbols-outlined text-[#8D4D3B] text-[16px]">radiology</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-[14px] font-semibold text-[#1D1B19]">Reflets et réseau vasculaire</span>
                  <span className="text-[13px] text-[#53433F]">
                    Évaluation simultanée de la pâleur et de la fatigue conjonctivale.
                  </span>
                </div>
              </div>
            </div>

            <p className="text-[13px] text-[#53433F] italic">
              Synthèse et unification des marqueurs bilatéraux… Élaboration de votre bilan global.
            </p>
          </section>
        )}

        {/* Error banner if any */}
        {errorMessage && (
          <div className="w-full bg-[#FFDAD6] text-[#93000A] rounded-2xl p-4 flex items-center gap-3">
            <span className="material-symbols-outlined text-[24px] text-[#93000A]">{errorMessage.icon}</span>
            <span className="text-[16px] font-bold">{errorMessage.text}</span>
          </div>
        )}

        {/* 6. Section des Résultats (visible si réponse reçue) */}
        {resultText && (
          <section ref={resultsCardRef} className="flex flex-col space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[#8D4D3B] text-[24px]">troubleshoot</span>
                <h2 className="text-[22px] font-bold text-[#1D1B19]">Résultats de l'analyse</h2>
              </div>
              <span className="text-[12px] text-[#53433F]">{resultTime}</span>
            </div>

            {/* Unified result card */}
            <div className="bg-white rounded-2xl p-5 shadow-[0px_4px_20px_-2px_rgba(61,58,56,0.06)] flex flex-col space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-full bg-[#BFEAC5] text-[#406749] flex items-center justify-center shrink-0">
                  <span className="material-symbols-outlined text-[26px] fill-1">verified</span>
                </div>
                <div>
                  <span className="text-[12px] text-[#406749] font-bold tracking-wide uppercase">
                    BILAN GLOBAL UNIFIÉ
                  </span>
                </div>
              </div>

              {/* Single text block from API */}
              <p className="text-[15px] leading-[24.375px] text-[#53433F] whitespace-pre-line">
                {resultText}
              </p>
            </div>

            {/* Sécurité et chiffrement */}
            <div className="flex items-center justify-center gap-2 py-2 px-3 text-center text-[#53433F]">
              <span className="material-symbols-outlined text-[18px] text-[#406749]">lock</span>
              <p className="text-[13px]">
                <strong className="font-semibold text-[#1D1B19]">Résultat enregistré en toute sécurité.</strong>{' '}
                Données médicales chiffrées de bout en bout sur votre appareil.
              </p>
            </div>
          </section>
        )}

        {/* 7. Avertissement médical (toujours visible en bas) */}
        <section className="bg-[#F9F2EF] rounded-2xl p-5 flex items-start gap-3">
          <div className="w-6 h-6 rounded-full bg-[#EDE7E4] flex items-center justify-center shrink-0 mt-0.5">
            <span className="material-symbols-outlined text-[#53433F] text-[16px]">info</span>
          </div>
          <p className="text-[13px] leading-[21px] text-[#53433F]">
            Ce résultat est une aide au dépistage et ne remplace pas un avis médical. En cas de doute, d'irritation persistante ou de gêne visuelle, parlez-en à votre ophtalmologue ou médecin traitant.
          </p>
        </section>
      </main>
    </div>
  );
}
