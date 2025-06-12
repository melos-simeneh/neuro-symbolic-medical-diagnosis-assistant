;; ==================================
;; Patient Sample Symptoms (Facts) 
;; ==================================

!(add-atom &self (: SYM1 (Evaluation has_symptom Abebe fever)))
!(add-atom &self (: SYM2 (Evaluation has_symptom Abebe cough)))
!(add-atom &self (: SYM3 (Evaluation has_symptom Abebe fatigue)))
!(add-atom &self (: SYM5 (Evaluation has_symptom Abebe loss_of_smell)))
!(add-atom &self (: SYM6 (Evaluation has_symptom Abebe chills)))
!(add-atom &self (: SYM7 (Evaluation has_symptom Abebe sneezing)))
!(add-atom &self (: SYM8 (Evaluation has_symptom Abebe sore_throat))) 


;; ======================
;; Diagnosis Rules
;; ======================

;; Flu: fever + cough + fatigue → flu
!(add-reduct &self (: flu-rule
  (-> (Evaluation has_symptom $p fever)
      (-> (Evaluation has_symptom $p cough)
          (-> (Evaluation has_symptom $p fatigue)
              (Result has_disease $p flu)))))
)

;; COVID-19: fever + cough + loss_of_smell → covid19
!(add-reduct &self (: covid-rule
  (-> (Evaluation has_symptom $p fever)
      (-> (Evaluation has_symptom $p cough)
          (-> (Evaluation has_symptom $p loss_of_smell)
              (Result has_disease $p covid19)))))
)

;; Malaria: fever + fatigue + chills → malaria
!(add-reduct &self (: malaria-rule
  (-> (Evaluation has_symptom $p fever)
      (-> (Evaluation has_symptom $p fatigue)
          (-> (Evaluation has_symptom $p chills)
              (Result has_disease $p malaria)))))
)

;; Common Cold: cough + sneezing + sore_throat → common_cold
!(add-reduct &self (: cold-rule
  (-> (Evaluation has_symptom $p cough)
      (-> (Evaluation has_symptom $p sneezing)
          (-> (Evaluation has_symptom $p sore_throat)
              (Result has_disease $p common_cold)))))
)

;; ========================================
;; 1. Natural Number Encoder (Peano Style)
;; ========================================
(= (fromNumber $n) 
   (if (<= $n 0) Z (S (fromNumber (- $n 1)))))

;; =======================================
;; 5. Reasoning Logic: Proof Construction
;; =======================================

(= (syn $kb $_ (: $prf $ccln)) 
   (match $kb (: $prf $ccln) (: $prf $ccln)))

(= (syn $kb (S $k) (: ($prfabs $prfarg) $ccln))
   (let* (
       ((: $prfabs (-> $prms $ccln)) (syn $kb $k (: $prfabs (-> $prms $ccln))))
       ((: $prfarg $prms) (syn $kb $k (: $prfarg $prms))))
     (: ($prfabs $prfarg) $ccln)))

