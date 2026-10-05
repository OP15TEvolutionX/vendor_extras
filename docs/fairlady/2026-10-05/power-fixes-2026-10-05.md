# Изменения энергосбережения fairlady / EvolutionX

5 октября 2026. Изменены исходники; установка на телефон не выполнялась.

## Idle Manager
LunarisIdleManager теперь проверяет enabled, destroyed и непустой список перед запуском цикла, назначением будильника, приёмом будильника, выполнением queued scan и перед применением действия. Очистка списка через API или Settings отменяет ожидающий будильник и инвалидирует поколение цикла. Добавление первой цели при выключенном экране запускает цикл. UID reconciliation тоже пропускается без целей. Последующее обновление ниже заменяет две проверки одной после заданного времени.
12 host-проверок исполняют реальный Java-класс с Android fakes и реальным libcore JSON: disabled/empty, две проверки вместо повторного ночного polling, отмена, запоздалый broadcast, queued scan после выключения или очистки списка, изменения Settings и добавление первой цели.

## LOW_POWER и DEVICE_IDLE
В QTI Power HAL добавлена device-gated поддержка обоих режимов. Soong-флаг включён только в fairlady/device.mk. Расширение Oplus для double-tap сохраняется.
Ресурсные профили в canoe/powerhint.xml используют AOSP LOW_POWER hint 0x1205, тип -1 для Battery Saver и отдельный тип 1 для Android DEVICE_IDLE. Независимые perf-lock handles; повторное включение не накапливает locks, выключение одного режима не снимает другой, ошибка acquisition сообщается вызывающей стороне и допускает повторную попытку. Mutex защищает конкурентные обращения. Прямых sysfs writes нет.
Начальные CPU ceilings около 2.61 GHz для обычного кластера и 3.40 GHz для prime. Значения ресурсов 2612/3399 MHz округлены вверх относительно bins 2611200/3398400 kHz из power_profile, чтобы не срезать целевой bin на округлении. Это стартовая политика, не результат измерения оптимальной эффективности. Оба режима используют одинаковые умеренные ceilings; min_freq и число online CPU не повышаются. Ограничения применяются только во время режимов; могут снижать скорость тяжёлой фоновой работы или работы в Battery Saver.
DEVICE_IDLE не подменяется штатным DISPLAY_DOZE hint 0x1053: состояние дисплея/AOD отдельно от idle Android. Thermal/perf HAL остаётся владельцем согласования ограничений.
Host C++-проверки реального PowerSavingModes: enable/disable, overlap, дубликаты, отказ acquisition/retry, destructor и 16 конкурентных callers. XML проверяется на соответствие hint type и только CPU ceilings. Реальная поддержка ресурсов в proprietary perf HAL и итоговые runtime-частоты ещё требуют устройства.

## Поднятие и сенсоры
PickupSensor/PocketSensor выбирают только wake-up вариант указанного сенсора. Регистрация идемпотентна, на главном потоке службы вместо отдельных executor threads. SCREEN_ON всегда снимает обе подписки; SCREEN_OFF и старт службы сверяют актуальные настройки. SharedPreferences listener и ContentObserver следят за жестами, DOZE_ENABLED и DOZE_ALWAYS_ON. onDestroy снимает listeners/observers. Запоздалые sensor events игнорируются после disable или при интерактивном экране. Pickup wakelock не reference-counted и освобождается при disable.
Host Kotlin-проверки компилируют реальные DozeService, Utils, PickupSensor, PocketSensor: выбор wake-up из двух вариантов, повторный старт, отсутствие пробуждений без sensor events, wake/pulse, выключение одного жеста при активном другом, stale event, SCREEN_ON/OFF, AOD, DOZE_ENABLED, teardown и отсутствие wake-up сенсора.
Vendor pickup_sensor_value=0 оставлен без изменения. Стандарт tilt_detector определяет значение 1; нужно увидеть фактический event vendor HAL, прежде чем менять это соответствие. Распознавание движения по-прежнему делегируется sensor HAL; программного polling акселерометра не добавлено.

## Проверка на телефоне
Сравнить actual governors/min/max до, во время и после Battery Saver/Device Idle; убедиться, что нет Failed to acquire power saving lock в логах. Проверить одновременный Battery Saver+idle и выход по отдельности. Проверить thermal ограничения, уведомления/звонки и время фоновых задач. Проверить sensorservice: wake-up flag, событие tilt 0/1 и отсутствие повторных событий при неподвижном телефоне. После подтверждения runtime сделать ночной A/B без постоянного ADB polling. Пока процент экономии неизвестен.

Итог проверки: финальные сборки SystemUI, OplusDoze и android.hardware.power-service-qti прошли. powerhint.xml собран в vendor/etc и побайтно совпадает с исходником. git diff --check пройден во всех четырёх изменённых проектах. Полная OTA успешно собрана; проверка на реальном устройстве ещё не выполнялась.

## Полная OTA
Сборка evolution_fairlady-userdebug, m evolution -j12: успешно, 11:27.
ZIP: out/target/product/fairlady/EvolutionX-17.0-20261005-fairlady-12.2-Unofficial.zip
Размер: 5145663277 байт. zipfile.testzip: CRC OK. OTA AB, SDK 37, patch 2026-09-01; pre-device OP64DDL1 совпадает с TARGET_OTA_ASSERT_DEVICE и build.prop.
SHA-256: a2d120a126300aff23e7a7a669db63d164eb52f8c201cced5780ed0c4413fad2
Лог: power-fixes-firmware-build.log. Контрольная сумма сохранена рядом с ZIP.

## Обновление Idle Manager: одна проверка
Удалена ранняя проверка через 30 секунд и повторная финальная проверка. Назначается один exact allow-while-idle wakeup alarm после заданных 1–240 минут от начала цикла screen-off. Новый default в службе и UI — 10 минут; CUSTOM сохранённый слайдер не перезаписывается, legacy BALANCED переводится в 10 минут. FULL_KILL на дедлайне не зависит от фонового lastTimeUsed. UID-gone FULL_KILL остаётся событийным механизмом без периодического polling.
Для остальных действий UsageStats запрашивается лениво один раз на весь проход; все приложения используют общий snapshot. Исключение запроса не приводит к повторам для каждого пакета. Пустой/null результат сохраняет прежнюю трактовку отсутствия usage.
Дедлайн проверяется при доставке alarm. Повторный broadcast в очереди не создаёт второй scan. Изменение timeout инвалидирует queued work и пересчитывает дедлайн от исходного screen-off; старый цикл не может завершить новый. Выключение и пустой список отменяют ожидание.
31 host-проверка реального Java-класса прошла, включая диапазон, defaults/migration, shared query/failure/null, individual lastUsed, stale/duplicate delivery и queued cycles.
Ранее собранный ZIP в разделе «Полная OTA» создан ДО этого обновления и новых изменений Idle Manager не содержит.

Проверка обновления: m SystemUIGoogle Settings -j12 для evolution_fairlady-userdebug завершена успешно (07:10). Лог idle-manager-single-scan-build.log. git diff --check пройден. Обновлённая полная OTA ещё не собиралась.

## OTA с одной проверкой Idle Manager
Сборка m evolution -j12 (evolution_fairlady-userdebug) прошла за 08:12.
Новый ZIP: out/target/product/fairlady/EvolutionX-17.0-20261005-fairlady-12.2-Unofficial.zip
Размер: 5290048112 байт. CRC всех ZIP entries: OK; pre-device OP64DDL1, OTA AB. Target-files APK Settings/SystemUIGoogle совпадают с актуальными установленными build outputs. В DEX найден Single scan after, старого First scan in 30 sec нет.
SHA-256: 9120bd13fa0e13b319da96f2e539da4c42930ca615b478d962347724a80fe1f5
Предыдущий ZIP сохранён в firmware-backups/before-idle-single-scan; checksum нового отличается. Лог idle-manager-single-scan-firmware-build.log. Проверка на телефоне ещё не выполнялась.
